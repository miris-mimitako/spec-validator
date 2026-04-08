describe("UserId", () => {
  it("rejects too short ids", () => {
    // domain-rule-001-LOWER-OUT-001
  });

  it("accepts minimum length ids", () => {
    // domain-rule-001-LOWER-IN-001
  });

  it("accepts maximum length ids", () => {
    // domain-rule-001-UPPER-IN-001
  });

  it("rejects too long ids", () => {
    // domain-rule-001-UPPER-OUT-001
  });

  it("rejects null", () => {
    // domain-rule-002-NULL-OUT-001
  });

  it("rejects empty string", () => {
    // domain-rule-002-EMPTY-OUT-001
  });

  it("accepts a valid id", () => {
    // domain-rule-002-VALID-IN-001
  });
});
