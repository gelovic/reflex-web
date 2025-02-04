"""UI and logic for the navbar component."""

from typing import Set

import reflex as rx
from pcweb import constants, styles
from pcweb.base_state import State
from reflex.vars import ImportVar, Var
from pcweb.components.logo import navbar_logo
from pcweb.components.sidebar import sidebar as sb

def shorten_to_k(number):
    if number >= 1000:
        return '{:.0f}k+'.format(number / 1000)
    else:
        return str(number)

    
class Search(rx.Component):
    tag = "InkeepCustomTrigger"

    special_props: Set[Var] = {Var.create_safe("{...inkeepCustomTriggerProps}")}

    is_open: Var[bool] = False

    def _get_imports(self):
        return {"next/dynamic": {ImportVar(tag="dynamic", is_default=True)}}

    def get_triggers(self) -> Set[str]:
        """Get the event triggers for the component.

        Returns:
            The event triggers.
        """
        return super().get_triggers() | {"on_close", "on_shortcutKey_pressed"}

    def _get_custom_code(self) -> str:
        return """ 
const InkeepCustomTrigger = dynamic(() => import("@inkeep/widgets").then((mod) => mod.InkeepCustomTrigger), { ssr: false });

const inkeepCustomTriggerProps = {
  baseSettings: {
    apiKey: '87b7469f79014c35a3313795088151a52de8a58a547abd16',
    integrationId: 'clkbf9e7e0001s601sa0ciax1',
    organizationId: 'org_WQKeNdnuPGEfuUhC',
    organizationDisplayName: 'Reflex',
    primaryBrandColor: '#5646ED',
    breadcrumbRules: {
      urlToBreadcrumbMapper: [
        {
          matchingRule: {
            ruleType: 'PartialUrl',
            partialUrl: 'reflex.dev/blog',
          },
          breadcrumbName: 'Blogs',
        },
        {
          matchingRule: {
            ruleType: 'PartialUrl',
            partialUrl: 'reflex.dev/docs',
          },
          breadcrumbName: 'Docs',
        },
        {
          matchingRule: {
            ruleType: 'PartialUrl',
            partialUrl: 'reflex.dev/docs/api-reference',
          },
          replaceLeading: true,
          breadcrumbName: 'API Reference',
        },
        {
          matchingRule: {
            ruleType: 'PartialUrl',
            partialUrl: 'reflex.dev/docs/library',
          },
          replaceLeading: true,
          breadcrumbName: 'Components Reference',
        },
      ],
    },
    stringReplacementRules: [
      {
        matchingRule: {
          ruleType: 'Substring',
          string: 'Api',
        },
        replaceWith: 'API',
        replaceInTitles: true,
      },
      {
        matchingRule: {
          ruleType: 'Substring',
          string: 'Cli',
        },
        replaceWith: 'CLI',
        replaceInTitles: true,
      },
    ],
  },
  modalSettings: {
    // optional typeof InkeepModalSettings
  },
  searchSettings: { // optional InkeepSearchSettings
    tabSettings: {
      isAllTabEnabled: true,
      useAllRootBreadcrumbsAsTabs: true,
      tabOrderByLabel: ['All', 'Docs', 'API Reference', 'Components Reference', 'Blogs'],
    },
    placeholder: 'Search documentation...',
  },
  aiChatSettings: { // optional typeof InkeepAIChatSettings
    quickQuestions: [
      'How does Reflex work?',
      'What types of apps can I build with Reflex?',
      'Where can I deploy my apps?',
    ],
  },
};
"""


inkeep = Search.create


class NavbarState(State):
    """The state for the navbar component."""

    # Whether the sidebar is open.
    sidebar_open: bool = False

    search_modal: bool = False

    search_input: str = ""

    enter: bool = False

    banner: bool = True

    def toggle_banner(self):

        self.banner = not self.banner

    def change_search(self):
        self.search_modal = not (self.search_modal)

    def toggle_sidebar(self):
        self.sidebar_open = not self.sidebar_open


def search_bar():
    return rx.hstack(
        rx.fragment(
            rx.icon(tag="search2", style=styles.NAV_SEARCH_STYLE),
            rx.text(
                "Search documentation...",
                style=styles.NAV_SEARCH_STYLE,
                font_weight=400,
            ),
        ),
        rx.spacer(),
        rx.text("/", style=styles.NAV_SEARCH_STYLE),
        on_click=NavbarState.change_search,
        display=["none", "flex", "flex", "flex", "flex"],
        min_width=["15em", "15em", "15em", "20em", "20em"],
        padding_x="1em",
        height="2em",
        border_radius="20px",
        bg="#FAF8FB",
    )


# Styles to use for the navbar.
logo_style = {
    "height": "1.25em",
}
logo = navbar_logo(**logo_style)


hover_button_style = {
    "_hover": {
        "background": "radial-gradient(82.06% 100% at 50% 100%, rgba(91, 77, 182, 0.04) 0%, rgba(234, 228, 253, 0.2) 100%), #FEFEFF;",
        "boxShadow": "0px 0px 0px 3px rgba(149, 128, 247, 0.6), 0px 2px 3px rgba(3, 3, 11, 0.2), 0px 4px 8px rgba(3, 3, 11, 0.04), 0px 4px 10px -2px rgba(3, 3, 11, 0.02), inset 0px 2px 0px rgba(255, 255, 255, 0.01), inset 0px 0px 0px 1px rgba(32, 17, 126, 0.4), inset 0px -20px 12px -4px rgba(234, 228, 253, 0.36);",
    },
}


def github_button():
    return rx.link(
        rx.hstack(
            rx.image(src="/companies/dark/github.svg", height="1.25em"),
            rx.text("Star", style=styles.NAV_TEXT_STYLE),
            rx.text(
                shorten_to_k(constants.GITHUB_STARS),
                color="#5646ED",
                bg="#F5EFFE",
                padding_x="0.5em",
                border_radius="6px",
                font_weight=600,
            ),
            box_shadow="0px 0px 0px 1px rgba(84, 82, 95, 0.14), 0px 1px 2px rgba(31, 25, 68, 0.14);",
            padding_x=".5em",
            height="2em",
            border_radius="8px",
            bg="#FFFFFF",
            style=hover_button_style,
        ),
        href=constants.GITHUB_URL,
        display=["none", "none", "none", "flex", "flex", "flex"],
    )


def discord_button():
    return rx.link(
        rx.center(
            rx.image(src="/companies/dark/discord.svg", height="1.25em"),
            box_shadow="0px 0px 0px 1px rgba(84, 82, 95, 0.14), 0px 1px 2px rgba(31, 25, 68, 0.14);",
            display=["none", "none", "none", "flex", "flex", "flex"],
            height="2em",
            width="2em",
            border_radius="8px",
            bg="#FFFFFF",
            style=hover_button_style,
        ),
        href=constants.DISCORD_URL,
    )


def navbar(sidebar: rx.Component = None) -> rx.Component:
    """Create the navbar component.

    Args:
        sidebar: The sidebar component to use.
    """
    # If the sidebar is not provided, create a default one.
    sidebar = sidebar or sb()

    # Create the navbar component.
    return rx.vstack(
        rx.cond(
            NavbarState.banner,
            rx.box(
                rx.hstack(
                    rx.center(
                        rx.box(
                            "✨ Announcing our seed funding led by Lux Capital!",
                            " Read more about it on our ",
                            rx.link(
                                "blog",
                                href="/blog/2023-08-02-seed-annoucement",
                                style={
                                    "color": "#FFFFFF",
                                    "text_decoration": "underline",
                                    "_hover": {"color": "#AD9BF8"},
                                },
                            ),
                            "  ✨",
                            color="#FFFFFF",
                            font_weight=600,
                        ),
                        width="100%",
                    ),
                    rx.spacer(),
                    rx.icon(
                        tag="close",
                        z_index=1000,
                        style={
                            "color": "#FFFFFF",
                            "text_decoration": "underline",
                            "_hover": {"color": "#AD9BF8"},
                        },
                        on_click=NavbarState.toggle_banner,
                    ),
                    width="100%",
                    padding_x=styles.PADDING_X,
                    align_items="center",
                ),
                background_color="#110F1F",
                padding_y=["0.8em", "0.8em", "0.5em"],
                width="100%",
            ),
        ),
        rx.box(
            rx.hstack(
                rx.hstack(
                    logo,
                    rx.link(
                        "Docs",
                        href="/docs/getting-started/introduction",
                        style=styles.NAV_TEXT_STYLE,
                        display=["none", "none", "none", "flex", "flex", "flex"],
                    ),
                    rx.link(
                        "Blog",
                        href="/blog",
                        style=styles.NAV_TEXT_STYLE,
                        display=["none", "none", "none", "flex", "flex", "flex"],
                    ),
                    rx.menu(
                        rx.menu_button(
                            rx.hstack(
                                rx.text("Resources", style=styles.NAV_TEXT_STYLE),
                                rx.icon(
                                    tag="chevron_down", style=styles.NAV_TEXT_STYLE
                                ),
                                cursor="pointer",
                                display=["none", "none", "none", "flex", "flex", "flex"],
                            )
                        ),
                        rx.menu_list(
                            rx.link(
                                rx.menu_item(
                                    "App Gallery", style=styles.NAV_DROPDOWN_STYLE
                                ),
                                href="/docs/gallery",
                            ),
                            rx.link(
                                rx.menu_item(
                                    "Roadmap", style=styles.NAV_DROPDOWN_STYLE
                                ),
                                href=constants.ROADMAP_URL,
                            ),
                            rx.link(
                                rx.menu_item("FAQ", style=styles.NAV_DROPDOWN_STYLE),
                                href="/faq",
                            ),
                            rx.menu_divider(),
                            rx.link(
                                rx.menu_item(
                                    "Contribute to Open Source",
                                    style=styles.NAV_DROPDOWN_STYLE,
                                ),
                                href=constants.CONTRIBUTING_URL,
                            ),
                            rx.link(
                                rx.menu_item(
                                    "Report A Bug",
                                    style=styles.NAV_DROPDOWN_STYLE,
                                ),
                                href=constants.REPORT_A_BUG_URL,
                            ),
                        ),
                    ),
                    spacing="2em",
                ),
                rx.hstack(
                    search_bar(),
                    inkeep(
                        is_open=NavbarState.search_modal,
                        on_close=NavbarState.change_search,
                    ),
                    github_button(),
                    discord_button(),
                    rx.icon(
                        tag="hamburger",
                        on_click=NavbarState.toggle_sidebar,
                        width="1.5em",
                        height="1.5em",
                        _hover={
                            "cursor": "pointer",
                            "color": styles.ACCENT_COLOR,
                        },
                        display=["flex", "flex", "flex", "none", "none", "none"],
                    ),
                    height="full",
                ),
                justify="space-between",
                padding_x=styles.PADDING_X,
            ),
            bg="rgba(255,255,255, 0.9)",
            backdrop_filter="blur(10px)",
            padding_y=["0.8em", "0.8em", "0.5em"],
            border_bottom="1px solid #F4F3F6",
            width="100%",
        ),
        rx.drawer(
            rx.drawer_overlay(
                rx.drawer_content(
                    rx.hstack(
                        logo,
                        rx.icon(
                            tag="close",
                            on_click=NavbarState.toggle_sidebar,
                            width="4em",
                            _hover={
                                "cursor": "pointer",
                                "color": styles.ACCENT_COLOR,
                            },
                        ),
                        justify="space-between",
                        margin_bottom="1.5em",
                    ),
                    sidebar if sidebar is not None else rx.text("Sidebar"),
                    padding_x="2em",
                    padding_top="2em",
                    bg="rgba(255,255,255, 0.97)",
                ),
                bg="rgba(255,255,255, 0.5)",
            ),
            placement="left",
            is_open=NavbarState.sidebar_open,
            on_close=NavbarState.toggle_sidebar,
            bg="rgba(255,255,255, 0.5)",
        ),
        position="sticky",
        z_index="999",
        top="0",
        width="100%",
        spacing="0",
    )
