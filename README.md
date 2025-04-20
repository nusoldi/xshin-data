setup

```ǹpm install```

run

``node xshin.js``

usage

```
usage:
  node xshin.js validator <pubkey>    - get data for a specific validator
  node xshin.js top [limit=10]        - get top validators
  node xshin.js award <category>      - get award winners (best_llv, best_skip_rate)
  node xshin.js all [pool|all]        - get all validators (pool-only or all)
  node xshin.js overview              - get overview data
```

awards
```
    best_skip_rate: best_skip_rate,
    best_cu: best_cu,
    best_latency: best_latency,
    best_llv: best_llv,
    best_cv: best_cv,
    best_vote_inclusion: best_vote_inclusion,
    best_apy: best_apy,
    best_pool_extra_lamports: best_pool_extra_lamports,
    best_city_concentration: best_city_concentration,
    best_country_concentration: best_country_concentration,
    best_overall: best_overall,
```
