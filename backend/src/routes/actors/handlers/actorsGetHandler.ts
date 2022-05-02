import postgres from "../../../db"

export default async function actorsGetHandler(actorId: number) {
  const results = await postgres.actorsMethods.getActor(actorId)
  return results
}
