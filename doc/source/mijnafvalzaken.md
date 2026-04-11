# HVCGroep

Support for schedules provided by [mijnafvalzaken.nl](https://www.mijnafvalzaken.nl/) and other Dutch municipalities.

## Configuration via configuration.yaml

```yaml
waste_collection_schedule:
  sources:
    - name: mijnafvalzaken_nl
      args:
        postal_code: POSTAL_CODE
        house_number: HOUSE_NUMBER
        service: SERVICE
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
# hvcgroep
waste_collection_schedule:
  sources:
    - name: hvcgroep_nl
      args:
        postal_code: 1713VM
        house_number: 1
        service: hvcgroep
```

```yaml
# cyclusnv
waste_collection_schedule:
  sources:
    - name: hvcgroep_nl
      args:
        postal_code: 2841ML
        house_number: 1090
        service: cyclusnv
```

```yaml
# apartment address with house_letter and suffix (30 A100)
waste_collection_schedule:
  sources:
    - name: hvcgroep_nl
      args:
        postal_code: 6531ED
        house_number: 30
        house_letter: A
        suffix: 100
        service: dar
```