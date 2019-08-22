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
        .package(url: "https://github.com/scinfu/SwiftSoup", from: "2.2.0")
    ],
    targets: [
        .target(
            name: "ParkImporter",
            dependencies: ["SwiftSoup"]),
        .testTarget(
            name: "ParkImporterTests",
            dependencies: ["ParkImporter"]),
    ]
)
