import { Type, Static } from "@sinclair/typebox"

export const SearchQuery = Type.Object({
  input: Type.String(),
})
export type SearchQueryType = Static<typeof SearchQuery>
