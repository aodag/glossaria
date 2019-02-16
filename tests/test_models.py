def test_it():
    from glossaria.models import Project, Glossary

    p = Project(name="testing")
    g = Glossary(project=p, name="testing-word", description="this is test")
    assert g.project == p
