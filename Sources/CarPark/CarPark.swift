public enum CarPark {
    public static var importers: [BaseDataSource] = [
        Dresden()
    ]

    public static func importer(forSourceWithName name: String) -> BaseDataSource? {
        importers.first { $0.name == name }
    }

    public static var supportedSources: [String] {
        importers.map { $0.name }
    }
}
