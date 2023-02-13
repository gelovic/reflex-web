import pynecone as pc

from pcweb.templates.docpage import doccode, docheader, docpage, doctext, subheader


@docpage()
def pages():
    return pc.box(
        docheader("Pages", first=True),
        doctext(
            "Pages specify the component to render for a given URL.",
        ),
        subheader("Adding a Page"),
        doctext(
            "You can create a page by defining a function that returns a component and adding the ",
            pc.code("pc.route"),
            " decorator. ",
        ),
        doctext(
            "By default, the function name will be used as the route, but you can also specify a route.",
        ),
        doccode(
            """
        @pc.route()
        def index():
            return pc.text('Root Page')

        @pc.route()
        def about():
            return pc.text('About Page')

        @pc.route("/custom-route")
        def custom():
            return pc.text('Custom Route')

        app = pc.App()
        app.compile()
    """
        ),
        doctext(
            "In this example we create three pages: ",
        ),
        doctext(
            pc.unordered_list(
                pc.vstack(
                    pc.list_item(
                        pc.code("index"),
                        " - The root route, available at ",
                        pc.code("/"),
                        width="100%",
                    ),
                    pc.list_item(
                        pc.code("about"),
                        " - available at ",
                        pc.code("/about"),
                        width="100%",
                    ),
                    pc.list_item(
                        pc.code("custom"),
                        " - available at ",
                        pc.code("/custom-route"),
                        width="100%",
                    ),
                )
            )
        ),
        subheader("Nested Routes"),
        doctext(
            "Pages can also have nested routes.",
        ),
        doccode(
            """
        @pc.route("/nested/page")
        def nested_page():
            return pc.text('Nested Page')

        app = pc.App()
        app.compile()
"""
        ),
        doctext(
            "This component will be available at ",
            pc.code("/nested/page"),
            ".",
        ),
        subheader("Dynamic Routes"),
        doctext(
            "For more complex applications, you may need a dynamic route that changes based on the URL. ",
        ),
        doctext(
            "You can specify dynamic arguments with square brackets in the route. ",
        ),
        doccode(
            """
class State(pc.State):
    @pc.var
    def post_id(self):
        return self.get_query_params().get("pid", "no pid")

@pc.route("/post/[pid]")
def post():
    \"""A page that updates based on the route.\"""
    return pc.heading(State.post_id)

app = pc.App(state=State)
app.compile()
"""
        ),
        doctext(
            "When you visit ",
            pc.code("/post/123"),
            ", the page will render with the text ",
            pc.code("123"),
            ".",
        ),
        doctext(
            "You can also specify multiple dynamic arguments, ",
            "and they will be available in the ",
            pc.code("get_query_params"),
            " dictionary.",
        ),
        doctext(
            "We also provide methods to get the current page, as well as the token of the user who made the request. ",
        ),
        doccode(
            """
class State(pc.State):
    @pc.var
    def post_id(self):
        return self.get_query_params().get("pid", "no pid")

    @pc.var
    def current_page(self):
        return self.get_current_page()

    @pc.var
    def token(self):
        return self.get_token()

@pc.route("/post/[pid]")
def post():
    \"""A page that updates based on the route.\"""
    return pc.vstack(
        pc.text(State.post_id), 
        pc.text(State.current_page),
        pc.text(State.token),
    )

app = pc.App(state=State)
app.compile()
"""
        ),
        subheader("Page Metadata"),
        doctext(
            "You can add page metadata such as: ",
        ),
        pc.unordered_list(
            pc.vstack(
                pc.list_item(
                    pc.text("The title that will appear in the browser tab"),
                    width="100%",
                ),
                pc.list_item(
                    pc.text("The description that will appear in search results"),
                    width="100%",
                ),
                pc.list_item(
                    pc.text(
                        "The image that will appear when the page is shared on social media"
                    ),
                    width="100%",
                ),
            )
        ),
        doccode(
            """
@pc.route(title="My Beautiful App", description="A beautiful app built with Pynecone", image="/splash.png")
def index():
    return pc.text('A Beautiful App')

@pc.route(title="About Page")
def about():
    return pc.text('About Page')

app = pc.App()
            """
        ),
        doctext(
            "The ",
            pc.code("pc.route"),
            " decorator is just a shortcut for ",
            pc.code("app.add_page"),
            ". ",
        ),
        doccode(
            """
        def index():
            return pc.text('Root Page')

        app = pc.App()
        app.add_page(index, route="/", title="My Beautiful App", description="A beautiful app built with Pynecone", image="/splash.png")
        app.compile()
        """
        ),
        subheader("Page Load Events"),
        doctext(
            "You can also specify a function to run when the page loads. ",
            "This can be useful for fetching data once vs on every render or state change.",
        ),
        doctext("In this example, we fetch data when the page loads:"),
        doccode(
            """
            class State(pc.State):
                data: Dict[str, Any]

                def get_data():
                    # Fetch data
                    self.data = fetch_data()

            @app.route(on_load=State.get_data)
            def index():
                return pc.text('A Beautiful App')
            """
        ),
    )
