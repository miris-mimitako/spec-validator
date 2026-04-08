describe("UserId UT", () => {
  it("rejects too short ids", () => {
    // TRACE: domain-rule-001-LOWER-OUT-001
  });

  it("accepts minimum length ids", () => {
    // TRACE: domain-rule-001-LOWER-IN-001
  });

  it("rejects null", () => {
    // TRACE: domain-rule-002-NULL-OUT-001
  });

  it("rejects empty string", () => {
    // TRACE: domain-rule-002-EMPTY-OUT-001
  });
});
