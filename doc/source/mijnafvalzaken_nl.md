# Mijn Afvalzaken

Support for schedules provided by [mijnafvalzaken.nl](https://www.mijnafvalzaken.nl/) for (BUCH Gemeente) Gemeente Bergen, Gemeente Uitgeest, Gemeente Castricum and Gemeente Heilo.

## Configuration via configuration.yaml

```yaml
waste_collection_schedule:
  sources:
    - name: mijnafvalzaken_nl
      args:
        postal_code: POSTAL_CODE
        house_number: HOUSE_NUMBER
```

### Configuration Variables

**postal_code**
*(string) (required)*

**house_number**
*(string) (required)*

**house_letter**
*(string) (optional)*

**suffix**
*(string) (optional)*

## Example

```yaml
# mijnafvalzaken
waste_collection_schedule:
  sources:
    - name: mijnafvalzaken_nl
      args:
        postal_code: 1911LB
        house_number: 14
```
