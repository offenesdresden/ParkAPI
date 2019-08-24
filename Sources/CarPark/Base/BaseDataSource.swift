import Foundation

public protocol BaseDataSource {
    var name: String { get }
    var slug: String { get }

//    var lots: [Lot] { get }

    var url: URL { get }
    var sourceURL: URL { get }

    func prepare(request: URLRequest) -> URLRequest

    func fetch(session: URLSession,
               completion: @escaping (Result<DataPoint, ParkError>) -> Void)
}

extension BaseDataSource {
    public var slug: String {
        return self.name.slug
    }

    public func prepare(request: URLRequest) -> URLRequest {
        return request
    }

    internal func fetchData(_ session: URLSession = .shared,
                               completion: @escaping (Result<(Data, URLResponse), Error>) -> Void) {
        var baseRequest = URLRequest(url: self.sourceURL)
        baseRequest.addValue("User-Agent", forHTTPHeaderField: "CarPark VERSION - Info: https://github.com/offenesdresden/ParkAPI")
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
