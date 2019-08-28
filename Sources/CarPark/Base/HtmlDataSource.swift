import Foundation

public protocol HtmlDataSource: BaseDataSource {
    var htmlEncoding: String.Encoding { get }

    func parse(html: String, response: HTTPURLResponse) throws -> DataPoint
}

extension HtmlDataSource {
    public var htmlEncoding: String.Encoding {
        return .utf8
    }

    public func fetch(session: URLSession = .shared,
                      completion: @escaping (Result<DataPoint, ParkError>) -> Void) {
        self.fetchData(session) { result in
            switch result {
            case .failure(let error):
                completion(.failure(.other(error)))
            case .success(let data, let response):
                guard let html = String(data: data, encoding: self.htmlEncoding) else {
                    completion(.failure(.decoding))
                    return
                }
                do {
                    let dataPoint = try self.parse(html: html, response: response as! HTTPURLResponse)
                    completion(.success(dataPoint))
                } catch {
                    completion(.failure(.other(error)))
                }
            }
        }
    }
}
