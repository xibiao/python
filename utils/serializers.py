
def model_to_dict(models, excludes=None):
    """支持批量模型转换的增强版"""
    if excludes is None:
        excludes = []
    if isinstance(models, list):
        return [{
            c.name: getattr(m, c.name)
            for c in m.__table__.columns
            if c.name not in excludes
        } for m in models]
    else:
        return {
            c.name: getattr(models, c.name)
            for c in models.__table__.columns
            if c.name not in excludes
        }

