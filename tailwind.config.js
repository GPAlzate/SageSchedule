module.exports = {
    purge: {
        enabled: true,
        content: [
            "./templates/index.html",
            "./static/css/main.css"
        ]
    },
    darkMode: false, // or 'media' or 'class'
    theme: {
        extend: {},
    },
    variants: {
        extend: {},
    },
    plugins: [],
}
