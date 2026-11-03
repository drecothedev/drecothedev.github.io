# Ciao! 👋🏽
 This is my portfolio website! 
 
 This is my first project using Agents and wow it is an experience. A part of me was very hesitant to use agents because i began taking a lot of pride in the craftsmanship of writing code. This project felt perfect because i am not the hugest fan of writing html and css code (tbh). It also taught me a lot about using multiple quality assurance agents to coordinate ideas and optimizations with the main coding agent. This project was an assignment for one of my classes where we build a website to sell products, hence the cart section. Instead of dollars, I try to calculate how long it will take to explore the code and high level thought behind the project. 

Thank you for taking the time, let me know if you have any questions or anything!


## Development

The root HTML, CSS, JavaScript, and `assets/` folder are the static GitHub Pages site. The canonical Flask source is in `submission/ActivityWebserver`. Keep template changes there, then regenerate the static preview:

```sh
python3 -m pip install -r submission/ActivityWebserver/requirements.txt
python3 scripts/verify_milestone2.py
python3 scripts/test_build_workflows.py
python3 scripts/export_milestone2_preview.py
cp -R portfolio/dist/. .
```

Commit the regenerated root files and source changes together. The static cart shows example exploration times; the Flask version recalculates session totals. `scripts/build_milestone2.py` is retired and intentionally refuses to overwrite source. `.nojekyll` lets GitHub Pages serve these static files without interpreting the Flask templates.

See `portfolio/README.md` and `reviews/QA-PROGRAMMER-HANDOFF.md` for the source layout and QA resolution.
