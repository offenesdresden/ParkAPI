public enum ParkImporter {
    public static var importers: [BaseImporter] = [
        Dresden()
    ]

    public static func importer(forSourceWithName name: String) -> BaseImporter? {
        return ParkImporter.importers.first { $0.name == name }
    }
}
