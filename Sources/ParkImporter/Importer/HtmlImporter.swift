import Foundation

public protocol HtmlImporter: BaseImporter {
    var htmlEncoding: String.Encoding { get }

    func parse(html: String, response: URLResponse) throws -> DataPoint
}

extension HtmlImporter {
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
                    let lotInfo = try self.parse(html: html, response: response)
                    completion(.success(lotInfo))
                } catch {
                    completion(.failure(.other(error)))
                }
            }
        }
    }
}
