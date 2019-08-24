import Foundation

public enum CarPark {
    public static var dataSources: [BaseDataSource] = [
        Dresden()
    ]

    public static func dataSource(forSourceWithName name: String) -> BaseDataSource? {
        dataSources.first { $0.name == name }
    }

    public static var supportedSources: [String] {
        dataSources.map { $0.name }
    }

    public static func gatherData(session: URLSession = .shared,
                                  completion: @escaping (Result<(BaseDataSource, DataPoint), ParkError>) -> Void) {
        dataSources.forEach { dataSource in
            dataSource.fetch(session: session) { result in
                switch result {
                case .failure(let error):
                    completion(.failure(error))
                case .success(let dataPoint):
                    completion(.success((dataSource, dataPoint)))
                }
            }
        }
    }
}
