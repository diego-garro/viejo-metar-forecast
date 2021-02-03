from rich.console import Console
from rich.theme import Theme

console = Console(width=100, theme=Theme({'repr.number': 'not bold'}))