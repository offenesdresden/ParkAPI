import Foundation

public protocol RssImporter: BaseImporter {
    func parse(rss: Data, response: URLResponse) throws -> DataPoint
}

extension RssImporter {
    public func fetch(session: URLSession = .shared,
                      completion: @escaping (Result<DataPoint, ParkError>) -> Void) {
        // TODO
    }
}
