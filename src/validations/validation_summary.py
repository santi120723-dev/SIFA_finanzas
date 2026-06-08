from src.logger import logger


def validation_summary(
    results: list,
) -> None:
    """
    Genera un resumen de las validaciones ejecutadas.
    """

    critical_passed = [
        result
        for result in results
        if (
            result.get("severity")
            == "CRITICAL"
            and result.get("status")
            == "passed"
        )
    ]

    warnings = [
        result
        for result in results
        if result.get("severity")
        == "WARNING"
    ]

    logger.info("=" * 50)

    logger.info(
        "VALIDATION SUMMARY"
    )

    logger.info(
        f"CRITICAL PASSED: "
        f"{len(critical_passed)}"
    )

    logger.info(
        f"WARNINGS: "
        f"{len(warnings)}"
    )

    if warnings:

        logger.info(
            "WARNING DETAILS:"
        )

        for warning in warnings:

            logger.info(
                warning.get(
                    "message",
                    "Sin detalle"
                )
            )

    logger.info("=" * 50)