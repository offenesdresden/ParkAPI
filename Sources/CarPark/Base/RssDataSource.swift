import Foundation

public protocol RssDataSource: BaseDataSource {
    func parse(rss: Data, response: URLResponse) throws -> DataPoint
}

extension RssDataSource {
    public func fetch(session: URLSession = .shared,
                      completion: @escaping (Result<DataPoint, ParkError>) -> Void) {
        // TODO
    }
}
