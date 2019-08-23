public enum ParkImporter {
    public static var importers: [BaseImporter] = [
        Dresden()
    ]

    public static func importer(forSourceWithName name: String) -> BaseImporter? {
        importers.first { $0.name == name }
    }

    public static var supportedSources: [String] {
        importers.map { $0.name }
    }
}
