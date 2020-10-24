import tkinter as tk
import math
import yaml
import tkinter.font as tk_font
from pygments import lex
from pygments.lexers import (PythonLexer, RustLexer, CLexer, CppLexer, JavaLexer, MarkdownLexer, CssLexer,
                             GoLexer, DockerLexer, YamlLexer, JavascriptLexer, HtmlDjangoLexer)

class SyntaxHighlighting():

    def __init__(self, parent, text_widget, initial_content):
        self.settings = parent.loader.load_settings_data()
        self.default_theme = parent.loader.load_default_theme()

        self.parent = parent
        self.text = text_widget
        self.font_family = parent.font_family
        self.font_size = parent.font_size
        self.previousContent = initial_content
        self.lexer = PythonLexer()

        self.comment_color = self.default_theme['comment_color']
        self.string_color = self.default_theme['string_color']
        self.number_color = self.default_theme['number_color']
        self.keyword_color = self.default_theme['keyword_color']
        self.operator_color = self.default_theme['operator_color']
        self.function_color = self.default_theme['function_color']
        self.class_color = self.default_theme['class_self_color']
        self.namespace_color = self.default_theme['namespace_color']
        self.object_color = self.default_theme['object_color']
        self.text_color = parent.font_color


    def default_highlight(self):
        row, _ = self.text.index(tk.INSERT).split('.')
        location = f'{row}.00'
        content = self.text.get("1.0", "end-1c")
        lines = content.split("\n")
        if (self.previousContent != content):
            self.text.mark_set("range_start", location)
            word = str(len(lines[int(row) - 1]))
            if int(word) < 10:
                data = self.text.get(location, row + ".0" + word)
            else:
                data = self.text.get(location, row + "." + word)
            for token, content in lex(data, self.lexer):
                self.text.mark_set("range_end", "range_start + %dc" % len(content))
                self.text.tag_add(str(token), "range_start", "range_end")
                self.text.mark_set("range_start", "range_end")
        self.previousContent = self.text.get("1.0", "end-1c")


    def initial_highlight(self, *args):
        self.clear_existing_tags()
        self.text.mark_set("range_start", "1.0")
        data = self.text.get("1.0", "end-1c")
        for token, content in lex(data, self.lexer):
            self.text.mark_set("range_end", "range_start + %dc" % len(content))
            self.text.tag_add(str(token), "range_start", "range_end")
            self.text.mark_set("range_start", "range_end")
        self.text.tag_configure('Token.Comment.Single', foreground=self.comment_color)
        self.text.tag_configure('Token.Comment.Multiline', foreground=self.comment_color)
        self.text.tag_configure('Token.Literal.String', foreground=self.string_color)
        self.text.tag_configure('Token.Literal.String.Char', foreground=self.string_color)
        self.text.tag_configure('Token.Literal.Number.Integer', foreground=self.number_color)
        self.text.tag_configure('Token.Literal.Number.Float', foreground=self.number_color)
        self.text.tag_configure('Token.Keyword', foreground=self.keyword_color)
        self.text.tag_configure('Token.Operator', foreground=self.operator_color)
        self.text.tag_configure('Token.Keyword.Type', foreground=self.keyword_color)
        self.text.tag_configure('Token.Keyword.Declaration', foreground=self.keyword_color)
        self.text.tag_configure('Token.Name.Class', foreground=self.object_color)
        self.text.tag_configure('Token.Text.Whitespace')
        self.text.tag_configure('Token.Name.Function', foreground=self.object_color)
        self.text.tag_configure('Token.Keyword.Namespace', foreground=self.namespace_color)
        self.text.tag_configure('Token.Generic.Emph', font=self.parent.italics)
        self.text.tag_configure('Token.Generic.Strong', font=self.parent.bold)
        self.text.tag_configure('Token.Generic.Heading', font=self.parent.header1)
        self.text.tag_configure('Token.Generic.Subheading', font=self.parent.header2)
        self.text.tag_configure('Token.Name.Builtin.Pseudo', foreground=self.class_color)
        self.text.tag_configure('Token.Name.Builtin', foreground=self.function_color)
        self.text.tag_configure('Token.Punctuation.Indicator', foreground=self.function_color)
        self.text.tag_configure('Token.Literal.Scalar.Plain', foreground=self.number_color)
        self.text.tag_configure('Token.Literal.String.Single', foreground=self.string_color)
        self.text.tag_configure('Token.Literal.String.Double', foreground=self.string_color)
        self.text.tag_configure('Token.Keyword.Constant', foreground=self.number_color)
        self.text.tag_configure('Token.Literal.String.Interpol', foreground=self.string_color)
        self.text.tag_configure('Token.Name.Decorator', foreground=self.number_color)
        self.text.tag_configure('Token.Operator.Word', foreground=self.operator_color)
        self.text.tag_configure('Token.Literal.String.Affix', foreground=self.function_color)
        self.text.tag_configure('Token.Name.Function.Magic', foreground=self.function_color)
        self.text.tag_configure('Token.Literal.Number.Oct', foreground=self.number_color)
        self.text.tag_configure('Token.Keyword.Reserved', foreground=self.keyword_color)
        self.text.tag_configure('Token.Name.Attribute', foreground=self.function_color)
        self.text.tag_configure('Token.Name.Tag', foreground=self.namespace_color)
        self.text.tag_configure('Token.Comment.Preproc', foreground=self.comment_color)
        self.text.tag_configure('Token.Comment.PreprocFile', forground=self.comment_color)
        self.text.tag_configure('Token.Name.Label', foreground=self.class_color)


    def load_new_theme(self, path):
        with open(path) as new_theme_config:
            new_config = yaml.load(new_theme_config, Loader=yaml.FullLoader)
        self.comment_color = new_config['comment_color']
        self.string_color = new_config['string_color']
        self.number_color = new_config['number_color']
        self.keyword_color = new_config['keyword_color']
        self.operator_color = new_config['operator_color']
        self.function_color = new_config['function_color']
        self.class_color = new_config['class_self_color']
        self.namespace_color = new_config['namespace_color']
        self.object_color = new_config['object_color']
        self.text_color = new_config['font_color']
        
        settings = self.parent.loader.load_settings_data()
        settings['text_selection_bg'] = new_config['selection_color']
        settings['insertion_color'] = new_config['font_color']
        settings['menu_fg'] = new_config['comment_color']
        settings['menu_bg'] = new_config['bg_color']
        settings['font_color'] = new_config['font_color']
        settings['textarea_background_color'] = new_config['bg_color']
        settings['menubar_active_bg'] = new_config['menu_bg_active']
        settings['menubar_active_fg'] = new_config['menu_fg_active']  
        settings['menu_active_bg'] = new_config['menu_bg_active']
        settings['menu_active_fg'] = new_config['menu_fg_active']

        self.parent.loader.store_settings_data(settings)
        self.parent.reconfigure_settings()
        self.initial_highlight()

    def clear_existing_tags(self):
        for tag in self.text.tag_names():
            self.text.tag_delete(tag)

    def load_python3_syntax(self):
        self.lexer = PythonLexer()
        self.initial_highlight()
        
    def load_c_syntax(self):
        self.lexer = CLexer()
        self.initial_highlight()

    def load_javascript_syntax(self):
        self.lexer = JavascriptLexer()
        self.initial_highlight()

    def load_cpp_syntax(self):
        self.lexer = CppLexer()
        self.initial_highlight()

    def load_html_syntax(self):
        self.lexer = HtmlDjangoLexer()
        self.initial_highlight()

    def load_css_syntax(self):
        self.lexer = CssLexer()
        self.initial_highlight()

    def load_go_syntax(self):
        self.lexer = GoLexer()
        self.initial_highlight()

    def load_markdown_syntax(self):
        self.lexer = MarkdownLexer()
        self.initial_highlight()
        
    def load_yaml_syntax(self):
        self.lexer = YamlLexer()
        self.initial_highlight()

    def load_java_syntax(self):
        self.lexer = JavaLexer()
        self.initial_highlight()

    def load_rust_syntax(self):
        self.lexer = RustLexer()
        self.initial_highlight()

    def load_docker_syntax(self):
        self.lexer = DockerLexer()
        self.initial_highlight()




