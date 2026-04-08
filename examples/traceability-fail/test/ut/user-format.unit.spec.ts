describe("User format UT", () => {
  it("accepts correctly formatted user id", () => {
    // TRACE: domain-rule-003-FORMAT-VALID-001
  });

  it("has malformed trace comment for invalid format", () => {
    // domain-rule-003-FORMAT-INVALID-001
  });

  it("rejects empty display name", () => {
    // TRACE: domain-rule-004-LOWER-OUT-001
  });

  it("accepts bio under the limit", () => {
    // TRACE: domain-rule-005-VALID-IN-001
  });
});
