class Store:
    def __init__(self, driver):

        self.driver = driver
        self.num_horses = len(driver.find_elements(
            'class name', 'content-name-title'))
        self.horses = [Horse(driver, i) for i in range(
            self.num_horses-1) if type(Horse(driver, i).price) == int]


class Horse:
    def __init__(self, driver, i):
        self.driver = driver
        price = (driver.find_elements(
            'class name', 'content-name-title')[i].text)
        name = (driver.find_elements('class name', 'item-info-title')[i].text)
        rarity, breed_type, gender = (driver.find_elements(
            'class name', 'item-info-meta')[i].text).replace(' ', '').split('•')

        auction_link = driver.find_elements('tag name', 'a')[
            i].get_attribute('href')

        try:
            self.price = int(price.replace(',', ''))
        except:
            self.price = price
        self.name = name
        self.rarity = rarity
        self.breed_type = breed_type
        self.gender = gender
        self.auction_link = auction_link
