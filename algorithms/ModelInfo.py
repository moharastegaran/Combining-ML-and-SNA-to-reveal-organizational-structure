class ModelInfo:
    def __init__(self, model, params, cv_scorer, features, pct):
        self.model = model
        self.params = params
        self.cv_scorer = cv_scorer
        self.features = features
        self.pct = pct