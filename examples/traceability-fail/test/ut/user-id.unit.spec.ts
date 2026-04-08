describe("UserId UT", () => {
  it("cannot go below minimum", () => {
    // TRACE: domain-rule-001-LOWER-OUT-OMITTED Reason: upstream parser blocks values shorter than three characters
  });

  it("accepts minimum length ids", () => {
    // TRACE: domain-rule-001-LOWER-IN-001
  });

  it("contains a malformed annotation comment", () => {
    // domain-rule-002-NULL-OUT-001
  });
});
