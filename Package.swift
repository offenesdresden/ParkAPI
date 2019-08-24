// swift-tools-version:5.1

import PackageDescription

let package = Package(
    name: "CarPark",
    products: [
        .library(
            name: "CarPark",
            targets: ["CarPark"]),
    ],
    dependencies: [
        .package(url: "https://github.com/scinfu/SwiftSoup", from: "2.2.0"),
        .package(url: "https://github.com/nmdias/FeedKit", from: "8.1.1"),
        .package(url: "https://github.com/JohnSundell/Files", from: "3.1.0"),
    ],
    targets: [
        .target(
            name: "CarPark",
            dependencies: ["SwiftSoup", "FeedKit"]),
        .target(
            name: "geojson",
            dependencies: ["Files", "CarPark"]),
        .testTarget(
            name: "CarParkTests",
            dependencies: ["CarPark"]),
    ]
)
