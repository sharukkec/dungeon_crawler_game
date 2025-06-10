import pycodestyle


def test_pep8_conformance():
    style = pycodestyle.StyleGuide()
    options = style.options
    options.ignore = 'E501'
    result = style.check_files(['battle.py', 'enemy.py', 'entity.py', 'game_over_screen.py', 'level.py', 'main.py',
                                'menu.py', 'player.py', 'settings.py', 'tile.py', 'ui.py'])
    assert result.total_errors == 0, "Found style errors (and warnings)."
