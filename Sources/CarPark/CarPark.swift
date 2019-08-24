import Foundation

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

    public static func gatherData(session: URLSession = .shared,
                                  completion: @escaping (Result<(BaseDataSource, DataPoint), ParkError>) -> Void) {
        importers.forEach { importer in
            importer.fetch(session: session) { result in
                switch result {
                case .failure(let error):
                    completion(.failure(error))
                case .success(let dataPoint):
                    completion(.success((importer, dataPoint)))
                }
            }
        }
    }
}
