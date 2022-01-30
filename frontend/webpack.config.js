const path = require("path");
const srcPath = path.resolve(__dirname, "src");

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
  },
   resolve: {
    extensions: [".jsx", ".js", ".tsx", ".ts"],
    alias: {
      "@components": path.resolve(srcPath, "components"),
      "@pages": path.resolve(srcPath, "pages"),
      "@actions": path.resolve(srcPath, "actions"),
      "@reducers": path.resolve(srcPath, "reducers"),
      "@hocs": path.resolve(srcPath, "hocs"),
    },
  },
};
