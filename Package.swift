// swift-tools-version:5.1

import PackageDescription

let package = Package(
    name: "ParkImporter",
    products: [
        .library(
            name: "ParkImporter",
            targets: ["ParkImporter"]),
    ],
    dependencies: [
        .package(url: "https://github.com/scinfu/SwiftSoup", from: "2.2.0"),
        .package(url: "https://github.com/nmdias/FeedKit", from: "8.1.1"),
    ],
    targets: [
        .target(
            name: "ParkImporter",
            dependencies: ["SwiftSoup", "FeedKit"]),
        .testTarget(
            name: "ParkImporterTests",
            dependencies: ["ParkImporter"]),
    ]
)
