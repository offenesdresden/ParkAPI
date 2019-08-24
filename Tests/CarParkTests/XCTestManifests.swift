import XCTest

#if !canImport(ObjectiveC)
public func allTests() -> [XCTestCaseEntry] {
    return [
        testCase(CarParkTests.allTests),
        testCase(SlugTests.allTests)
    ]
}
#endif
