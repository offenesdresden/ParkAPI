import XCTest

#if !canImport(ObjectiveC)
public func allTests() -> [XCTestCaseEntry] {
    return [
        testCase(ParkImporterTests.allTests),
        testCase(SlugTests.allTests)
    ]
}
#endif
