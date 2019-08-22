import Foundation

public enum ParkImporter {
    public static var importers: [BaseImporter] = [
        Dresden()
    ]
}

// MARK: - Base Importer

public protocol BaseImporter {
    var name: String { get }
    var slug: String { get }

//    var lots: [Lot] { get }

    var url: URL { get }
    var sourceURL: URL { get }

    func prepare(request: URLRequest) -> URLRequest

    func fetch(session: URLSession,
               completion: @escaping (Result<LotInformation, ParkError>) -> Void)
}

extension BaseImporter {
    public var slug: String {
        return self.name.slug
    }

    public func prepare(request: URLRequest) -> URLRequest {
        return request
    }

    fileprivate func fetchData(_ session: URLSession = .shared,
                               completion: @escaping (Result<(Data, URLResponse), Error>) -> Void) {
        var baseRequest = URLRequest(url: self.sourceURL)
        baseRequest.addValue("User-Agent", forHTTPHeaderField: "ParkImporter VERSION - Info: https://github.com/offenesdresden/ParkAPI")
        let request = prepare(request: baseRequest)

        let task = session.dataTask(with: request) { data, response, error in
            if let data = data, error == nil {
                completion(.success((data, response!)))
                return
            } else if let error = error, data == nil {
                completion(.failure(error))
                return
            }
            assertionFailure("Expected to receive either data or error from URLSessionDataTask.")
        }

        task.resume()
    }
}

// MARK: - HTML Importer

public protocol HtmlImporter: BaseImporter {
    var htmlEncoding: String.Encoding { get }

    func parse(html: String, response: URLResponse) throws -> LotInformation
}

extension HtmlImporter {
    public var htmlEncoding: String.Encoding {
        return .utf8
    }

    public func fetch(session: URLSession = .shared,
                      completion: @escaping (Result<LotInformation, ParkError>) -> Void) {
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

// MARK: - RSS Importer

public protocol RssImporter: BaseImporter {
    func parse(rss: Data, response: URLResponse) throws -> LotInformation
}

extension RssImporter {
    public func fetch(session: URLSession = .shared,
                      completion: @escaping (Result<LotInformation, ParkError>) -> Void) {
        // TODO
    }
}
