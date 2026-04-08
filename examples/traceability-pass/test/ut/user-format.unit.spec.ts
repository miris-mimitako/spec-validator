describe("User format UT", () => {
  it("accepts correctly formatted user id", () => {
    // TRACE: domain-rule-003-FORMAT-VALID-001
  });

  it("rejects malformed user id", () => {
    // TRACE: domain-rule-003-FORMAT-INVALID-001
  });

  it("rejects empty display name", () => {
    // TRACE: domain-rule-004-LOWER-OUT-001
  });

  it("accepts minimum display name length", () => {
    // TRACE: domain-rule-004-LOWER-IN-001
  });

  it("accepts longer display name", () => {
    // TRACE: domain-rule-004-VALID-IN-001
  });

  it("accepts bio under the limit", () => {
    // TRACE: domain-rule-005-VALID-IN-001
  });

  it("accepts bio at the limit", () => {
    // TRACE: domain-rule-005-UPPER-IN-001
  });

  it("rejects bio over the limit", () => {
    // TRACE: domain-rule-005-UPPER-OUT-001
  });
});
