describe("UserId IT", () => {
  it("accepts maximum length ids", () => {
    // TRACE: domain-rule-001-UPPER-IN-001
  });

  it("accepts a valid id", () => {
    // TRACE: domain-rule-002-VALID-IN-001
  });

  it("has a combination test without TRACE-RULES", () => {
    // TRACE: domain-rule-002-COMBO-VALID-001
  });

  it("has a combination test with incomplete TRACE-RULES", () => {
    // TRACE: domain-rule-002-COMBO-INVALID-001
    // TRACE-RULES: domain-rule-002, domain-rule-003
  });

  it("has an unmapped stray id", () => {
    // TRACE: domain-rule-123-LOWER-IN-001
  });
});
