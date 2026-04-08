describe("UserId", () => {
  it("cannot go below minimum", () => {
    // domain-rule-001-LOWER-OUT-OMITTED Reason: upstream parser blocks values shorter than three characters
  });

  it("accepts minimum length ids", () => {
    // domain-rule-001-LOWER-IN-001
  });

  it("accepts maximum length ids", () => {
    // domain-rule-001-UPPER-IN-001
  });

  it("accepts a valid id", () => {
    // domain-rule-002-VALID-IN-001
  });

  it("has an unmapped stray id", () => {
    // domain-rule-123-LOWER-IN-001
  });
});
