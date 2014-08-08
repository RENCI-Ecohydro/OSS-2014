# RENCI - Ecohydrology Project
Last update: August 1, 2014

## Introduction

Loss of forest cover from varying disturbance types can result in changes in a watersheds physical characteristics that directly impact stream flow regimes and biogeochemical qualities. Adams et al (2011) performed a comprehensive review of the ecohydrological effects associated to forest die-off and found that tree mortality results in altered evaporation, transpiration, and canopy interception which all indirectly alter watershed hydrological processes. They found in drier systems, loss of canopy increases evapotranspiration to levels that can significantly decrease water yield. Alternatively, in wetter systems where annual precipitation exceeds ~ 500mm and is dominated by snowmelt, annual water yields increase, raising concern for erosion and flood risk. In terms of chemical processes within watersheds, Mikkelson et al (2012) demonstrated increases in organic carbon concentrations within municipal water supplies that had been perturbed by tree mortatlity associated with mountain pine beetle infestation due to increased particulate transport in defoliated forests. 

## Statistical Analysis Methods

This section describes the statistical methodology portion of the disturbance effects modeling. 

### Response variables

Water Quantity Metrics:  
For the measures of change in the total annual flow from pre-disturbance to post-disturbance, we collected the following response variables before and after the specified forest cover loss year. 

1. Change in cumulative annual flow $\Delta CAF$ 
2. Change in peak annual flow $\Delta PAF$

### Predictor variables

Watershed level covariates ($i,k$)  

1. percent forest loss
2. size of watershed in m$^2$  
3. forest cover type (Conifer, Deciduous, Mixed, Other)

Climate level covariates ($j$)

1. spatial kriged classification of climate type by flow

Other potential predictors: 

4. Change in 5 year mean annual precipitation $\Delta ppt$
5. Change in 5 year mean annual temperature $\Delta T_{mean}$

### Hierarchical Bayesian Structure
###Model:

$$Y_{ijk} \sim N(\mu_{ijk}, \sigma)\quad \text{where} \quad Y_{ijk} =\Delta CAF$$ 
####$$ \quad i = \text{watershed} , \quad j = \text{climate class}, \quad k = \text{forest type (1=con., 2=decid., 3=mix, 4 = other)} $$

$$\mu_{ijk} = \beta_{0jk} + \beta_{1jk}x_{1ijk} + \beta_{2jk}x_{2ijk}  $$
$$\quad\text{where} \quad x_{1} = \text{percent forest loss}, \quad x_{2} = \text{watershed size}$$

###Priors:

$$\beta_{jk} \sim N(\mu_{\beta_{jk}}, \sigma_{jk})$$
$$\mu_{\beta k j} \sim N(0, \sigma_{\tau})$$
$$\sigma, \sigma_{jk}, \sigma_{\tau} \sim \text{Half Cauchy(100)}$$
