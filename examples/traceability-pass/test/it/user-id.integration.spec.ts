describe("UserId IT", () => {
  it("accepts maximum length ids", () => {
    // TRACE: domain-rule-001-UPPER-IN-001
  });

  it("accepts a valid combination from the length perspective", () => {
    // TRACE: domain-rule-001-COMBO-VALID-001
    // TRACE-RULES: domain-rule-001, domain-rule-002
  });

  it("rejects an invalid combination from the length perspective", () => {
    // TRACE: domain-rule-001-COMBO-INVALID-001
    // TRACE-RULES: domain-rule-001, domain-rule-002
  });

  it("applies boundary priority from the length perspective", () => {
    // TRACE: domain-rule-001-COMBO-PRIORITY-001
    // TRACE-RULES: domain-rule-001, domain-rule-002
  });

  it("accepts a valid id", () => {
    // TRACE: domain-rule-002-VALID-IN-001
  });

  it("accepts a valid combination", () => {
    // TRACE: domain-rule-002-COMBO-VALID-001
    // TRACE-RULES: domain-rule-001, domain-rule-002
  });

  it("rejects an invalid combination", () => {
    // TRACE: domain-rule-002-COMBO-INVALID-001
    // TRACE-RULES: domain-rule-001, domain-rule-002
  });

  it("applies required-before-boundary priority", () => {
    // TRACE: domain-rule-002-COMBO-PRIORITY-001
    // TRACE-RULES: domain-rule-001, domain-rule-002
  });
});
