import spoonacular as sp


class ComplexSearch:

	def __init__(self,queryStr):
		self.api = sp.API("e49afb82519a407db4b10de35ddf7252")
		self.queryStr = queryStr
		self.query = None
		self.cuisine = None
		self.number = 10
		self.titleMatch = None
		self.includeIngredients = None
		self.diet = None
		self.type = None

	def search(self):
		propArgs = {
		'query':self.query,
		'cuisine':self.cuisine,
		'number':self.number,
		'diet':self.diet,
		'type':self.type,
		'includeIngredients':self.includeIngredients
		}
		return propArgs



	cuisineDefs = [
	"African","American",
	"British",
	"Cajun","Caribbean","Chinese",
	"Eastern European","European",
	"French",
	"German","Greek"
	"Indian","Irish","Italian",
	"Japanese","Jewish",
	"Korean",
	"Latin American",
	"Mediterranean","Mexican","Middle Eastern",
	"Nordic",
	"Southern","Spanish",
	"Thai",
	"Vietnamese"
	]

	dietDefs = [
	"Gluten Free",
	"Ketogenic",
	"Vegetarian",
	"Lacto-Vegetarian",
	"Ovo-Vegetarian",
	"Vegan",
	"Pescetarian",
	"Paleo",
	"Primal",
	"Whole30"
	]

	mealTypes = [
	"main course",
	"side dish",
	"dessert",
	"appetizer",
	"salad",
	"bread",
	"breakfast",
	"soup",
	"beverage",
	"sauce",
	"marinade",
	"fingerfood",
	"snack",
	"drink",
	]



