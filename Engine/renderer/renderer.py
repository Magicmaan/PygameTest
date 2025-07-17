import pygame
from Engine.InputHandler import InputHandler
from Engine.debug import Logger
from Engine.util import Vector2

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# from OpenGL.GL import *
from OpenGL.GL.shaders import *
from OpenGL.arrays import *
import OpenGL.GL as GL
import ctypes
from ctypes import c_float as GLfloat, c_uint as GLuint
from .utils import GLQuad, Utils


glsl_vert = """
    #version 450 core

    layout (location = 0) in vec3 a_pos;
    layout (location = 1) in vec3 a_nv;
    layout (location = 2) in vec3 a_uv;

    out vec3 v_pos;
    out vec3 v_nv;
    out vec3 v_uv;

    uniform mat4 u_proj;
    uniform mat4 u_view;
    uniform mat4 u_model;

    void main()
    {
        mat4 model_view = u_view * u_model;
        mat3 normal     = transpose(inverse(mat3(model_view)));

        vec4 view_pos   = model_view * vec4(a_pos.xyz, 1.0);

        v_pos       = view_pos.xyz;
        v_nv        = normal * a_nv;  
        v_uv        = a_uv;  
        gl_Position = u_proj * view_pos;
    }
"""

glsl_frag = """
    #version 450 core

    out vec4 frag_color;
    in  vec3 v_pos;
    in  vec3 v_nv;
    in  vec3 v_uv;

    layout (binding = 0) uniform sampler2DArray u_texture;

    const vec3 sideColor[6] = vec3[6](
        vec3(1.0, 0.0, 0.0),
        vec3(0.0, 1.0, 0.0),
        vec3(0.0, 0.0, 1.0),
        vec3(1.0, 1.0, 0.0),
        vec3(1.0, 0.0, 1.0),
        vec3(0.0, 1.0, 1.0)
    );

    void main()
    {
        vec3  N            = normalize(v_nv);
        vec3  V            = -normalize(v_pos);
        float ka           = 0.1;
        float kd           = max(0.0, dot(N, V)) * 0.9;
        vec4  textureColor = texture(u_texture, v_uv.xyz);
        vec3  color        = mix(sideColor[int(v_uv.z + 0.5)].rgb, textureColor.rgb, textureColor.a);
        frag_color         = vec4(color.rgb * (ka + kd), 1.0);
    }
"""

image_planes = [
    (GLubyte * 4)(255, 0, 0, 255),
    (GLubyte * 4)(0, 255, 0, 255),
    (GLubyte * 4)(0, 0, 255, 255),
    (GLubyte * 4)(255, 255, 0, 255),
    (GLubyte * 4)(0, 255, 255, 255),
    (GLubyte * 4)(255, 0, 255, 255),
]
image_size = (1, 1)


class BaseRenderer:
    """
    Base class for the renderer.
    """

    def __init__(
        self, game_resolution: pygame.Vector2, render_resolution: pygame.Vector2 = None
    ):
        self.logger = Logger.get_logger("Renderer")

        pygame.init()
        self._resolution = game_resolution
        self._render_resolution = render_resolution or Vector2(1920, 1080)
        self._render_scale = self.render_resolution / game_resolution

        self._surface = pygame.Surface(self.resolution, flags=pygame.SRCALPHA)
        self._window = pygame.display.set_mode(
            self.render_resolution, pygame.RESIZABLE | pygame.SRCALPHA
        )

        self._render_order = [
            "background",
            "foreground",
            "particles",
            "GUI",
            "debug",
        ]
        self.framerate = 60

        self._running = False
        self._render_layers = {
            "background": pygame.Surface(self.resolution),
            "foreground": pygame.Surface(self.resolution),
            "particles": pygame.Surface(self.resolution),
            "GUI": pygame.Surface(self.resolution, flags=pygame.SRCALPHA),
            "debug": pygame.Surface(self.render_resolution, flags=pygame.SRCALPHA),
        }
        self._tool_layers = {
            "light": pygame.Surface(self.resolution, flags=pygame.SRCALPHA),
            "collision": pygame.Surface(self.resolution, flags=pygame.SRCALPHA),
        }
        self.sprite_buffer: dict[str, list[object]] = {}
        for key in list(self._tool_layers.keys()) + list(self._render_layers.keys()):
            self.sprite_buffer[key] = []

        for layer in list(self._tool_layers.keys()) + list(self._render_layers.keys()):
            layer_surface = self._render_layers.get(layer) or self._tool_layers.get(
                layer
            )
            if layer_surface:
                layer_surface.fill((0, 0, 0, 0))
                layer_surface.set_colorkey((0, 0, 0, 0))

        pygame.display.set_caption("PTol")
        pygame.display.set_icon(pygame.Surface((1, 1)))  # Set a dummy icon
        pygame.display.set_caption("PTol: Pygame Renderer")
        pygame.display.set_window_position((50, 50))
        self.initialise()

        self.logger.debug("Renderer initialised")

    def clear_screen(self):
        """
        Clear the screen and all render layers.
        """
        self._surface.fill((0, 255, 0))

        for layer in self._render_layers.values():
            layer.fill((0, 0, 0))
        for layer in self._tool_layers.values():
            layer.fill((0, 0, 0))

    @property
    def width(self):
        return self._resolution.x

    @property
    def height(self):
        return self._resolution.y

    @property
    def resolution(self):
        return self._resolution

    @property
    def render_resolution(self):
        return self._render_resolution

    @property
    def render_scale(self):
        return self._render_scale

    @property
    def render_order(self):
        """
        Get the render order.
        This is the order in which the layers are rendered.
        """
        return self._render_order

    @property
    def surface(self):
        """
        Get the games output surface.
        This is the pixel buffer of the game in the games resolution.
        """
        return self._surface

    @property
    def window(self):
        """
        Get the games window surface.
        This is the surface that is displayed on the screen.
        """
        return self._window

    @property
    def render_layers(self):
        """
        Get the render layers.
        These are the layers that are rendered to the screen.
        """
        return self._render_layers

    @property
    def tool_layers(self):
        """
        Get the tool layers.
        These are the layers that are used for tools and debugging.
        """
        return self._tool_layers

    def initialise(self):
        """
        Initialise the renderer.
        Implement this method in the derived class.
        """
        pass

    def update(self, delta, tick):
        """
        Update the renderer.
        Implement this method in the derived class.
        """
        pass

    def draw(self):
        """
        Draw the renderer.
        Implement this method in the derived class.
        """
        pass

    def add_group_to_layer(self, group: object, layer: str):
        """
        Add a group of sprites to be rendered to a layer.
        """
        if not (layer in self._render_layers or layer in self._tool_layers):
            self.logger.error(
                f"Layer {layer} does not exist in render_layers or tool_layers"
            )
            return

        if not hasattr(group, "draw"):
            self.logger.error(
                f"Group {group} does not have 'draw' method. Cannot add to layer {layer}."
            )
            return

        self.sprite_buffer[layer].append(group)

    def remove_group_from_layer(self, group: object, layer: str):
        """
        Remove a group of sprites from a layer.
        """
        if layer in self.sprite_buffer and group in self.sprite_buffer[layer]:
            self.sprite_buffer[layer].remove(group)
        else:
            self.logger.error(
                f"Group {group} not found in layer {layer}. Cannot remove."
            )

    def add_layer(self, name: str, category: str = "tool"):
        """
        Add a new render layer.
        note: a layer cannot be removed once created."""
        if name not in self._render_layers:
            self._render_layers[name] = pygame.Surface(
                self.resolution, flags=pygame.SRCALPHA
            )
            self.sprite_buffer[name] = []
        else:
            print(f"Layer {name} already exists")

    def get_layer(self, name: str) -> pygame.Surface | None:
        """
        Get a layer by name.

        :return: The layer surface or None if it does not exist.
        """
        if name in self._render_layers:
            return self._render_layers[name]
        elif name in self._tool_layers:
            return self._tool_layers[name]
        else:
            print(f"Layer {name} does not exist")
            return None


def create_quad_vertices(quads: list[GLQuad]) -> tuple[list, list]:
    vertices: list[list[float]] = []
    indices: list[list[float]] = []

    for i, quad in enumerate(quads):
        # Base index for this quad
        base = i * 4

        # Get texture index or use 0 as default
        tex_index = getattr(quad, "texture_index", 0)

        # Vertices for this quad (x, y, z, s, t, tex_index)
        quad_verts = [
            # Position (relative to quad position and size)      # Texture coords      # Texture index
            quad.position[0],
            quad.position[1],
            0.0,
            quad.texture_coords[0],
            quad.texture_coords[1],
            float(tex_index),  # Top left
            quad.position[0],
            quad.position[1] - quad.size[1],
            0.0,
            quad.texture_coords[0],
            quad.texture_coords[3],
            float(tex_index),  # Bottom left
            quad.position[0] + quad.size[0],
            quad.position[1] - quad.size[1],
            0.0,
            quad.texture_coords[2],
            quad.texture_coords[3],
            float(tex_index),  # Bottom right
            quad.position[0] + quad.size[0],
            quad.position[1],
            0.0,
            quad.texture_coords[2],
            quad.texture_coords[1],
            float(tex_index),  # Top right
        ]
        vertices.extend(quad_verts)

        # Indices for this quad
        quad_indices = [
            base + 0,
            base + 1,
            base + 2,  # First triangle
            base + 0,
            base + 2,
            base + 3,  # Second triangle
        ]
        indices.extend(quad_indices)

    return vertices, indices


class GLRenderer(BaseRenderer):
    """
    The games renderer class.
    """

    vs_code = """
        #version 330 core
        layout (location = 0) in vec3 aPos;
        layout (location = 1) in vec2 aTexCoord;
        layout (location = 2) in float aTexIndex;
        
        out vec2 TexCoord;
        out float TexIndex;
        
        void main()
        {
            gl_Position = vec4(aPos, 1.0);
            TexCoord = aTexCoord;
            TexIndex = aTexIndex;
        }
    """
    # fragment shader code
    fs_code = """
        #version 330 core
        out vec4 FragColor;
        in vec2 TexCoord;
        in float TexIndex;
        
        uniform sampler2D texture0;
        uniform sampler2D texture1;
        uniform sampler2D texture2;
        uniform sampler2D texture3;
        uniform sampler2D texture4;
        
        void main()
        {
            vec4 texColor;
            int texIdx = int(TexIndex);
            
            if (texIdx == 0) {
                texColor = texture(texture0, TexCoord);
            } else if (texIdx == 1) {
                texColor = texture(texture1, TexCoord);
            } else if (texIdx == 2) {
                texColor = texture(texture2, TexCoord);
            } else if (texIdx == 3) {
                texColor = texture(texture3, TexCoord);
            } else if (texIdx == 4) {
                texColor = texture(texture4, TexCoord);
            } else {
                texColor = texture(texture0, TexCoord);
            }
            
            vec4 combined = vec4(texColor.rgb, 1.0);
            FragColor = combined;
        }
    """
    texID = None
    _textures: list[int] = []

    def surfaceToTexture(self, surface: pygame.Surface, texture_id: int = None):
        if not texture_id:
            # Create a texture object
            texture_id = glGenTextures(1)
            self._textures.append(texture_id)

        rgb_surface = pygame.image.tobytes(surface, "RGB")
        glBindTexture(GL_TEXTURE_2D, texture_id)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        surface_rect = surface.get_rect()
        glTexImage2D(
            GL_TEXTURE_2D,
            0,
            GL_RGB,
            surface_rect.width,
            surface_rect.height,
            0,
            GL_RGB,
            GL_UNSIGNED_BYTE,
            rgb_surface,
        )
        glGenerateMipmap(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, texture_id)

        return texture_id

    def drawGroup(self, group: pygame.sprite.Group, surface: pygame.Surface):
        for spr in group.sprites():
            if hasattr(spr, "draw"):
                spr.draw(surface)

    num_indices = 0

    def initialise(self):
        pygame.display.set_caption("PTol: OpenGL Renderer")
        # Indicate rendering details
        display_flags = pygame.DOUBLEBUF | pygame.OPENGL
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 1)
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, 4)
        pygame.display.gl_set_attribute(
            pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE
        )
        self.sprite_buffer: dict[str, list[object]] = {}
        for key in list(self.tool_layers.keys()) + list(self.render_layers.keys()):
            self.sprite_buffer[key] = []

        # Create and display the window
        self._window = pygame.display.set_mode(self.render_resolution, display_flags)

        self._program = Utils.initialize_program(self.vs_code, self.fs_code)

        # Set up vertex array object and buffers for a textured quad
        self._VAO = GL.glGenVertexArrays(1)
        self._VBO = GL.glGenBuffers(1)
        self._EBO = GL.glGenBuffers(1)

        self.quads: list[GLQuad] = []
        # self.num_indices = 0
        self.update_buffers()  # Initial buffer setup

        self.add_quad(GLQuad((-1, 1.0), (2, 2), self.texID, (0, 0, 1, 1)))

        # self.add_quad(GLQuad((0, 0), (1, 1), self.texID, (0, 0, 1, 1)))

        # Set the text that appears in the title bar of the window
        pygame.display.set_caption("Graphics Window")
        # Determine if main loop is active
        self._running = True
        # Manage time-related data and operations
        self._clock = pygame.time.Clock()
        # Manage user input
        self._input = InputHandler.getInstance()
        # number of seconds application has been running
        self._time = 0

        # Print the system information
        Utils.print_system_info()

    def update_buffers(self):
        if not self.quads:
            return

        vertices, indices = create_quad_vertices(self.quads)

        # Convert to appropriate format for OpenGL
        vertices_array = (GLfloat * len(vertices))(*vertices)
        indices_array = (GLuint * len(indices))(*indices)

        # Bind VAO
        GL.glBindVertexArray(self._VAO)

        # Update VBO
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self._VBO)
        GL.glBufferData(
            GL.GL_ARRAY_BUFFER,
            ctypes.sizeof(vertices_array),
            vertices_array,
            GL.GL_DYNAMIC_DRAW,
        )

        # Update EBO
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, self._EBO)
        GL.glBufferData(
            GL.GL_ELEMENT_ARRAY_BUFFER,
            ctypes.sizeof(indices_array),
            indices_array,
            GL.GL_DYNAMIC_DRAW,
        )

        # Position attribute (x, y, z)
        GL.glVertexAttribPointer(
            0, 3, GL.GL_FLOAT, GL.GL_FALSE, 6 * ctypes.sizeof(GLfloat), None
        )
        GL.glEnableVertexAttribArray(0)

        # Texture coordinate attribute (s, t)
        GL.glVertexAttribPointer(
            1,
            2,
            GL.GL_FLOAT,
            GL.GL_FALSE,
            6 * ctypes.sizeof(GLfloat),
            ctypes.c_void_p(3 * ctypes.sizeof(GLfloat)),
        )
        GL.glEnableVertexAttribArray(1)

        # Texture index attribute
        GL.glVertexAttribPointer(
            2,
            1,
            GL.GL_FLOAT,
            GL.GL_FALSE,
            6 * ctypes.sizeof(GLfloat),
            ctypes.c_void_p(5 * ctypes.sizeof(GLfloat)),
        )
        GL.glEnableVertexAttribArray(2)

        # Unbind
        GL.glBindVertexArray(0)

        # Store the number of indices for drawing
        self.num_indices = len(indices) or 0
        # self.logger.debug(f"Updated buffers with {len(self.quads)} quads.")

    def screen_normalised(self, pos: tuple[float, float]) -> tuple[float, float]:
        """Convert screen coordinates to normalised screen coordinates in the range 0 to 1."""
        x = pos[0] / self.output_resolution.x
        y = pos[1] / self.output_resolution.y
        return x, y

    def game_normalised(self, pos: tuple[float, float]) -> tuple[float, float]:
        """Convert game coordinates to normalised screen coordinates in the range 0 to 1."""
        x = ((pos[0]) / self.resolution.x) * 2
        y = ((pos[1]) / self.resolution.y) * 2
        return x, y

    def add_quad(self, quad: GLQuad):
        """
        Add a quad to the renderer.
        """
        self.quads.append(quad)
        self.update_buffers()

    def remove_quad(self, quad: GLQuad):
        """
        Remove a quad from the renderer.
        """
        if quad in self.quads:
            self.quads.remove(quad)
            self.update_buffers()
        else:
            self.logger.error(f"Quad {quad} not found in quads. Cannot remove.")

    def get_quad(self, index: int) -> GLQuad | None:
        """
        Get a quad by index.
        """
        if 0 <= index < len(self.quads):
            return self.quads[index]
        else:
            self.logger.error(f"Quad index {index} out of range. Cannot get quad.")
            return None

    def load_texture(self, surface: pygame.Surface) -> int:
        """
        Load a texture from a pygame surface and return its texture index

        :param surface: The pygame surface to load as a texture
        :return: The index of the texture in the texture array
        """
        # Create a texture object
        texture_id = glGenTextures(1)

        # Add to our textures list and get its index
        self._textures.append(texture_id)
        texture_index = len(self._textures) - 1

        # Convert and upload the surface
        rgb_surface = pygame.image.tobytes(surface, "RGB")
        glBindTexture(GL_TEXTURE_2D, texture_id)

        # Set texture parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)

        # Upload texture data
        surface_rect = surface.get_rect()
        glTexImage2D(
            GL_TEXTURE_2D,
            0,
            GL_RGB,
            surface_rect.width,
            surface_rect.height,
            0,
            GL_RGB,
            GL_UNSIGNED_BYTE,
            rgb_surface,
        )
        glGenerateMipmap(GL_TEXTURE_2D)

        return texture_index

    def draw_pygame(self):
        self.clear_screen()
        # draw all sprites to all layers
        # done this way since a sprite can be in multiple layers
        # and we want to draw them all
        for key, object_list in self.sprite_buffer.items():
            if len(object_list) == 0:
                continue
            for object in object_list:
                if hasattr(object, "draw"):
                    # Check if the key exists in render_layers
                    if key in self.render_layers:

                        surface = self.render_layers[key]

                        if isinstance(object, pygame.sprite.Group):
                            for sprite in object.sprites():
                                sprite.draw(surface)
                        else:
                            object.draw(surface)
                    # Check if the key exists in tool_layers
                    if key in self.tool_layers:
                        surface = self.tool_layers[key]
                        object.draw(surface)
                else:
                    self.logger.error(
                        f"Object {object} does not have 'draw' method. Cannot draw."
                    )

        # draw layers in order
        for i, layer in enumerate(self.render_layers):
            self.surface.blit(self.render_layers[layer], (0, 0))

        # apply render scale
        scaled_surface = pygame.transform.scale(self.surface, self.render_resolution)

        return scaled_surface

    def draw(self):
        # self._input.update()

        # Render the pygame content to a surface
        surface = self.draw_pygame()
        # Create texture from pygame surface if not already created
        if not self.texID:
            self.texID = self.surfaceToTexture(surface)
        else:
            self.surfaceToTexture(surface, self.texID)

        # Clear screen
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Use our shader program
        GL.glUseProgram(self._program)

        # Set texture uniforms
        for i, texture_id in enumerate(self._textures):
            # Set the uniform sampler to the appropriate texture unit
            loc = GL.glGetUniformLocation(self._program, f"texture{i}")
            GL.glUniform1i(loc, i)

            # Activate and bind texture
            glActiveTexture(GL_TEXTURE0 + i)
            glBindTexture(GL_TEXTURE_2D, texture_id)

        # Bind VAO
        GL.glBindVertexArray(self._VAO)

        # Draw all quads at once
        GL.glDrawElements(GL.GL_TRIANGLES, self.num_indices, GL.GL_UNSIGNED_INT, None)

        # Cleanup
        GL.glBindVertexArray(0)
        GL.glUseProgram(0)

        # Unbind textures
        for i in range(len(self._textures)):
            glActiveTexture(GL_TEXTURE0 + i)
            glBindTexture(GL_TEXTURE_2D, 0)

        pygame.display.flip()


class GLPoint(GLRenderer):
    def initialise(self):
        super().initialise()

        # render settings (optional) #
        # Set point width and height
        GL.glPointSize(10)


class PygameRenderer(BaseRenderer):
    """
    The games renderer class.
    """

    def initialise(self):

        self._window = pygame.display.set_mode(
            self.render_resolution, pygame.RESIZABLE | pygame.SRCALPHA
        )

        self.sprite_buffer: dict[str, list[object]] = {}
        for key in list(self.tool_layers.keys()) + list(self.render_layers.keys()):
            self.sprite_buffer[key] = []

        self.logger.debug("Pygame Renderer initialised")

    def setRenderSize(self, size: pygame.Vector2):
        """
        Set the render size of the renderer.
        """
        assert size.x > 0 and size.y > 0, "Render size must be greater than 0"
        self.resolution.update(size.x, size.y)
        self.render_scale.update(self.render_resolution / self.resolution)
        self.resolution = size

    def draw(self):
        self.clear_screen()

        # draw all sprites to all layers
        # done this way since a sprite can be in multiple layers
        # and we want to draw them all
        for key, object_list in self.sprite_buffer.items():
            if len(object_list) == 0:
                continue
            for object in object_list:
                if hasattr(object, "draw"):
                    # Check if the key exists in render_layers
                    if key in self.render_layers:
                        surface = self.render_layers[key]

                        if isinstance(object, pygame.sprite.Group):
                            for sprite in object.sprites():
                                sprite.draw(surface)
                        else:
                            object.draw(surface)
                    # Check if the key exists in tool_layers
                    if key in self.tool_layers:
                        surface = self.tool_layers[key]
                        object.draw(surface)
                else:
                    self.logger.error(
                        f"Object {object} does not have 'draw' method. Cannot draw."
                    )

        # draw layers in order
        for i, layer in enumerate(self.render_order):
            self.surface.blit(self.render_layers[layer], (0, 0))

        # apply render scale
        scaled_surface = pygame.transform.scale(self.surface, self.render_resolution)

        pygame.draw.rect(
            self._window,
            (0, 255, 0),
            (0, 0, self.render_resolution.x, self.render_resolution.y),
        )
        # draw to output surface
        self._window.blit(scaled_surface, self.window.get_rect())
        self._window.blit(self.render_layers.get("debug"), (0, 0))

        pygame.display.flip()
