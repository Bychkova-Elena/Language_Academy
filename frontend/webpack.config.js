module.exports = {
  module: {
    rules: [
      {
        test: /\.([tj])sx?$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader"
        }
      }
    ]
  }
};