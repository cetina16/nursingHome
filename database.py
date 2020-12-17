from disease import Disease

class Database:
    def __init__(self):
        self.diseases = {}
        self._last_movie_key = 0

    def add_disease(self, disease):
        self._last_movie_key += 1
        self.diseases[self._last_movie_key] = disease
        return self._last_movie_key

    def delete_disease(self, disease_key):
        if disease_key in self.diseases:
            del self.diseases[disease_key]

    def update_disease(self, disease_key, disease):
        self.diseases[disease_key] = disease

    def get_disease(self, disease_key):
        disease = self.diseases.get(disease_key)
        if disease is None:
            return None
        disease_ = Disease(disease.name,risklevel=disease.risklevel, period=disease.period)
        return disease_

    def get_diseases(self):
        diseases = []
        for disease_key, disease in self.diseases.items():
            disease_ = Disease(disease.name ,risklevel=disease.risklevel, period=disease.period)
            diseases.append((disease_key, disease_))
        return diseases