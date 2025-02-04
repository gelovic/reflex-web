import reflex as rx

config = rx.Config(
    port=3000,
    app_name="pcweb",
    api_url="https://reflex-web-bx4g-dev.fl0.io:8000",
    deploy_url="https://reflex-web-bx4g-dev.fl0.io",
    frontend_packages=[
        "react-confetti",
        "react-colorful",
        "react-copy-to-clipboard",
        "chakra-react-select",
        "@radix-ui/react-navigation-menu",
        "@tailwindcss/typography",
        "@splinetool/react-spline", 
        "@splinetool/runtime",
        "@inkeep/widgets@0.2.164",
    ], 
    telemetry_enabled=False,
    tailwind={
        "plugins": [
            "@tailwindcss/typography",
        ],
    },
)
