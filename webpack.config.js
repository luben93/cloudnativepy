module.exports = {
    entry: "./static/main.js",
    output: {
        path: __dirname + "/static/build/",
        filename: "bundle.js"

    },
    resolve: {
        extensions: ['.js', '.jsx']

    },
    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/,

                use: [{
                    loader: 'babel-loader',
                    options:{presets:['react','es2015']}
                }]
            }

        ]

    }

};
