from django.template import Template
from django.utils.translation import gettext_lazy

from iommi.experimental.main_menu import (
    EXTERNAL,
    M,
    MainMenu,
    path,
)
from tests.helpers import (
    req,
    show_output,
    show_output_collapsed,
)

request = req('get')

import pytest
pytestmark = pytest.mark.django_db


# language=rst
"""
.. _cookbook-main-menu:

Main menu
---------

"""

albums_view = edit_album_view = things_view = artists_view = lambda request, **_: None


def test_include(staff_user):
    # language=rst
    """
    How do I control which menu items are shown for a user?
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    .. uses M.include

    Using `include` you can control which menu items are shown for a given user. This also controls access, so you can know that your menu and your access control are always in sync.
    """

    menu = MainMenu(
        items=dict(
            albums=M(
                view=albums_view,
            ),
            artists=M(
                view=artists_view,
                include=lambda user, **_: user.is_staff,
            ),
        ),
    )

    # @test
    show_output(menu)
    # @end

    # @test
    show_output(menu, user=staff_user)
    # @end


def test_display_name():
    # language=rst
    """
    How do I control the display name of a menu item?
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    .. uses M.display_name

    By default the display name is derived from the `name` of the `M` object. So given:
    """

    menu = MainMenu(
        items=dict(
            albums=M(view=albums_view),
        ),
    )

    # @test
    show_output(menu)
    # @end

    # language=rst
    """
    The `name` would be "albums", and the display name is automatically derived as "Albums". The translation from `name` to `display_name` replaces `_` with space, runs `gettext_lazy()` on the result, and then capitalizes that.
    
    If you want to do something else, pass the `display_name` parameter:
    """

    menu = MainMenu(
        items=dict(
            albums=M(
                view=albums_view,
                display_name=gettext_lazy('Discography'),
            ),
        ),
    )

    # @test
    show_output(menu)
    # @end

    # language=rst
    """
    Note that `display_name` can be a function too.
    """


def test_paths():
    # language=rst
    """
    How do I add sub-paths for a menu item?
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    .. uses M.paths

    Since the menu system can control access, it is useful to nest path mappings under a specific menu item without showing them in the menu. This is done with the `paths` argument:
    """

    menu = MainMenu(
        items=dict(
            albums=M(
                view=albums_view,
                paths=[
                    path('<album_pk>/edit/', edit_album_view),
                ],
            ),
        ),
    )

    # @test
    show_output_collapsed(menu)
    # @end


def test_external_links():
    # language=rst
    """
    How do I add external links in the menu?
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    .. uses M.url
    .. uses EXTERNAL

    Use the special value `EXTERNAL` for the `view` argument, and use `url` argument:
    """

    menu = MainMenu(
        items=dict(
            albums=M(
                view=EXTERNAL,
                url='https://docs.iommi.rocks',
            ),
        ),
    )

    # @test
    show_output(menu)
    # @end

    # language=rst
    """
    Note the icon added by default for an external link. This is configurable via the `icon_formatter` on your `Style`.
    """


def test_nesting():
    # language=rst
    """
    How do I nest menu items?
    ~~~~~~~~~~~~~~~~~~~~~~~~~
    .. uses M.items
    .. uses M.open

    You can create a menu hierarchy with the `items` argument, which produces expandable sections. iommi will open the menu items that matches the current URL by default. You can also force a submenu to be open with the `open` argument:
    """

    menu = MainMenu(
        items=dict(
            things=M(
                view=things_view,
                open=True,  # force open
                items=dict(
                    albums=M(
                        view=albums_view,
                    ),
                    artists=M(
                        view=artists_view,
                    )
                ),
            ),
        ),
    )

    # @test
    show_output(menu)
    # @end

    # language=rst
    """
    The `open` argument can be a callable.
    """


def test_template():
    # language=rst
    """
    How do I put arbitrary html in the menu?
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    .. uses M.template

    With the `template` argument you can put arbitrary html into menu items:
    """

    menu = MainMenu(
        items=dict(
            albums=M(
                view=EXTERNAL,
                template=Template('''
                <li style="margin-left: 1rem">
                    <span style="display: inline-block; width: 1.5rem; background: red; border-radius: 50%">&nbsp;</span>
                    <span style="display: inline-block; width: 1.5rem; background: orange; border-radius: 50%">&nbsp;</span>
                    <span style="display: inline-block; width: 1.5rem; background: yellow; border-radius: 50%">&nbsp;</span>
                    <span style="display: inline-block; width: 1.5rem; background: green; border-radius: 50%">&nbsp;</span>
                    <span style="display: inline-block; width: 1.5rem; background: blue; border-radius: 50%">&nbsp;</span>
                </li>
                ''')
            ),
        ),
    )

    # @test
    show_output(menu)
    # @end

    # language=rst
    """
    Note that you want to include the `<li>` tag.
        
    You can also override the base template via your `Style`. 
    """


# url + path + params
# (i18n with okrand?)
