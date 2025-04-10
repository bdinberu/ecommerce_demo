
cube('products_js',{

  sql_table: "\"ECOM\".\"PRODUCTS\"",
  access_policy: [
    {
      role: `*`,
      conditions: [
        { if: securityContext.is_project_level }
      ],
      member_level: {
        includes: `*`
      }
    }
  ],
  measures: {},
  dimensions: {
    id: {
      sql: `${CUBE}."ID"`,
      type: `number`,
      primaryKey: true
    },
    name: {
      sql: `${CUBE}."NAME"`,
      type: `string`
    }
  }


});