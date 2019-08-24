import XCTest
@testable import CarPark

final class CarParkTests: XCTestCase {
    func testGetSpecificDataSource() {
        let dresden = CarPark.dataSource(forSourceWithName: "Dresden")
        XCTAssertEqual(dresden?.url.absoluteString, "https://www.dresden.de/parken")
    }

    func testSupportedSources() {
        XCTAssertEqual(CarPark.supportedSources.count, 1)
    }

    func testDataSourceProperties() {
        for dataSource in CarPark.dataSources {
            XCTAssert(!dataSource.name.isEmpty)
            XCTAssert(!dataSource.slug.isEmpty)
            XCTAssert(!dataSource.url.absoluteString.isEmpty)
            XCTAssert(!dataSource.sourceURL.absoluteString.isEmpty)
        }
    }

    func testLiveData() {
        guard !(ProcessInfo.processInfo.environment["TEST_LIVE"]?.isEmpty ?? true) else {
            print("Skipping live tests, set TEST_LIVE environment variable to enable.")
            return
        }

        for dataSource in CarPark.dataSources {
            let e = expectation(description: "Receive data for \(dataSource.name).")

            dataSource.fetch(session: .shared) { result in
                switch result {
                case .failure(let error):
                    XCTFail("Failed with error: \(error)")
                    e.fulfill()
                case .success(let dataPoint):
                    XCTAssert(!dataPoint.lots.isEmpty)
                    e.fulfill()
                }
            }

            waitForExpectations(timeout: 10)
        }
    }

    static var allTests = [
        ("testGetSpecificDataSource", testGetSpecificDataSource),
        ("testSupportedSources", testSupportedSources),
        ("testDataSourceProperties", testDataSourceProperties),
        ("testLiveData", testLiveData),
    ]
}
