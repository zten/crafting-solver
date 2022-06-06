from csolv import model
from csolv.model import SimpleCrafter, Action


def run():
    recipe = model.Recipe("Rarefied Integral Fishing Rod",
                          3500,
                          80,
                          7200,
                          90,
                          560,
                          130,
                          90,
                          115,
                          80)

    crafter = SimpleCrafter(90, 3316, 3211, 550)

    progress = Action('Basic Synthesis', 1.2, 0.0).get_progress(
        recipe.base_progress(crafter))
    quality = Action('Basic Touch', 0.0, 1.0).get_quality(recipe.base_quality(crafter))

    print(progress)
    print(quality)


if __name__ == '__main__':
    run()
