// swift-tools-version:5.1
// The swift-tools-version declares the minimum version of Swift required to build this package.

import PackageDescription

let package = Package(
  name: "tests",
  dependencies: [
    .package(url: "https://github.com/docopt/docopt.swift", from: "0.6.6"),
  ],
  targets: [
    .target(name: "tests", dependencies: ["docopt"]),
  ])
